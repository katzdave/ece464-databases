import { useState, useEffect } from 'react'
import { api } from './lib/api'
import { connectRoom } from './lib/ws'
import './App.css'

interface Player {
  id: string
  display_name: string
}

interface RoomState {
  code: string
  phase: string
  host_id: string
  players: Player[]
}

function App() {
  const [screen, setScreen] = useState<'home' | 'room'>('home')
  const [displayName, setDisplayName] = useState(
    () => localStorage.getItem('displayName') ?? ''
  )
  const [joinCode, setJoinCode] = useState('')
  const [userId, setUserId] = useState<string | null>(
    () => localStorage.getItem('userId')
  )
  const [room, setRoom] = useState<RoomState | null>(null)
  const [error, setError] = useState('')

  // Persist displayName to localStorage on change
  useEffect(() => {
    localStorage.setItem('displayName', displayName)
  }, [displayName])

  // --- User identity helpers ---

  async function createFreshUser(): Promise<string> {
    const data = await api.post<{ id: string }>('/users', {
      display_name: displayName,
    })
    localStorage.setItem('userId', data.id)
    localStorage.setItem('displayName', displayName)
    setUserId(data.id)
    return data.id
  }

  async function ensureUser(): Promise<string> {
    const storedId = localStorage.getItem('userId')
    const storedName = localStorage.getItem('displayName')
    if (storedId && storedName === displayName) {
      setUserId(storedId)
      return storedId
    }
    return createFreshUser()
  }

  // --- WebSocket: replace polling ---

  useEffect(() => {
    if (screen !== 'room' || !room) return
    const { close } = connectRoom(room.code, (raw) => {
      const msg = raw as { type: string; data: RoomState }
      if (msg.type === 'room_state') {
        setRoom(msg.data)
      }
    })
    return close
  }, [screen, room?.code])

  // --- Session restoration on mount ---

  useEffect(() => {
    const roomCode = sessionStorage.getItem('roomCode')
    const savedId = localStorage.getItem('userId')
    if (!roomCode || !savedId) return

    api
      .get<RoomState>(`/rooms/${roomCode}`)
      .then((data) => {
        if (data.players.some((p) => p.id === savedId)) {
          setUserId(savedId)
          setRoom(data)
          setScreen('room')
        } else {
          sessionStorage.removeItem('roomCode')
        }
      })
      .catch(() => sessionStorage.removeItem('roomCode'))
  }, [])

  // --- Actions ---

  async function handleCreate() {
    setError('')
    if (!displayName.trim()) {
      setError('Enter a display name')
      return
    }

    let uid: string
    try {
      uid = await ensureUser()
    } catch {
      setError('Failed to create user')
      return
    }

    try {
      const data = await api.post<{ code: string }>('/rooms', {
        host_id: uid,
      })
      const state = await api.get<RoomState>(`/rooms/${data.code}`)
      setRoom(state)
      sessionStorage.setItem('roomCode', data.code)
      setScreen('room')
    } catch (err) {
      // Retry once with a fresh user in case the stored userId is stale
      try {
        const freshUid = await createFreshUser()
        const data = await api.post<{ code: string }>('/rooms', {
          host_id: freshUid,
        })
        const state = await api.get<RoomState>(`/rooms/${data.code}`)
        setRoom(state)
        sessionStorage.setItem('roomCode', data.code)
        setScreen('room')
      } catch {
        setError(err instanceof Error ? err.message : 'Failed to create room')
      }
    }
  }

  async function handleJoin() {
    setError('')
    if (!displayName.trim()) {
      setError('Enter a display name')
      return
    }
    if (!joinCode.trim()) {
      setError('Enter a room code')
      return
    }

    let uid: string
    try {
      uid = await ensureUser()
    } catch {
      setError('Failed to create user')
      return
    }

    const code = joinCode.trim().toUpperCase()
    try {
      await api.post(`/rooms/${code}/join`, { user_id: uid })
      const state = await api.get<RoomState>(`/rooms/${code}`)
      setRoom(state)
      sessionStorage.setItem('roomCode', code)
      setScreen('room')
    } catch (err) {
      // Retry once with a fresh user in case the stored userId is stale
      try {
        const freshUid = await createFreshUser()
        await api.post(`/rooms/${code}/join`, { user_id: freshUid })
        const state = await api.get<RoomState>(`/rooms/${code}`)
        setRoom(state)
        sessionStorage.setItem('roomCode', code)
        setScreen('room')
      } catch {
        setError(err instanceof Error ? err.message : 'Failed to join room')
      }
    }
  }

  async function handleAdvance() {
    if (!room || !userId) return
    try {
      await api.post(`/rooms/${room.code}/advance`, { host_id: userId })
      // No need to fetchRoom — server broadcast delivers the update via WS
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to advance phase')
    }
  }

  function handleLeave() {
    sessionStorage.removeItem('roomCode')
    setScreen('home')
    setRoom(null)
  }

  if (screen === 'home') {
    return (
      <div style={{ maxWidth: 400, margin: '80px auto', textAlign: 'center' }}>
        <h1>Jackbox Clone</h1>
        <input
          placeholder="Display name"
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
          style={{
            display: 'block',
            width: '100%',
            padding: 8,
            marginBottom: 12,
            boxSizing: 'border-box',
          }}
        />
        <button
          onClick={handleCreate}
          style={{ width: '100%', padding: 10, marginBottom: 8 }}
        >
          Create Room
        </button>
        <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
          <input
            placeholder="Room code"
            value={joinCode}
            onChange={(e) => setJoinCode(e.target.value.toUpperCase())}
            maxLength={4}
            style={{ flex: 1, padding: 8 }}
          />
          <button onClick={handleJoin} style={{ padding: '8px 16px' }}>
            Join Room
          </button>
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </div>
    )
  }

  // Room screen
  const isHost = userId === room?.host_id

  return (
    <div style={{ maxWidth: 500, margin: '40px auto', textAlign: 'center' }}>
      <h1>Room: {room?.code}</h1>
      <p>
        Phase: <strong>{room?.phase}</strong>
      </p>

      <h2>Players ({room?.players.length})</h2>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {room?.players.map((p) => (
          <li key={p.id} style={{ padding: '4px 0' }}>
            {p.display_name} {p.id === room.host_id ? '(host)' : ''}
          </li>
        ))}
      </ul>

      {isHost && room?.phase !== 'finished' && (
        <button
          onClick={handleAdvance}
          style={{ padding: '10px 24px', marginTop: 16 }}
        >
          Advance Phase
        </button>
      )}

      <div style={{ marginTop: 32 }}>
        <button onClick={handleLeave} style={{ padding: '8px 16px' }}>
          Leave Room
        </button>
      </div>
    </div>
  )
}

export default App
