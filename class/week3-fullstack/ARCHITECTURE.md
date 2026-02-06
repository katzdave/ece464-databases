# Animal Explorer - Architecture Documentation

## System Overview

Animal Explorer is a full-stack web application demonstrating modern software architecture patterns. It uses a React frontend communicating with a FastAPI backend via REST APIs.

```
┌─────────────────────────────────────────────────────────┐
│                     Browser Client                       │
│  ┌────────────────────────────────────────────────────┐ │
│  │              React Application                     │ │
│  │  (Components, State Management, API Client)        │ │
│  └────────────────────────────────────────────────────┘ │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTP/JSON (CORS enabled)
                        │ Port 5173 → 8000
┌───────────────────────▼─────────────────────────────────┐
│                  FastAPI Backend                         │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Routes → Business Logic → Data Access             │ │
│  │  (Pydantic Models, Type Validation)                │ │
│  └────────────────────────────────────────────────────┘ │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
                  Hard-coded Data
              (In-memory Python dict)
```

## Backend Architecture

### Technology Stack
- **Framework**: FastAPI 0.115+
- **Server**: Uvicorn (ASGI)
- **Validation**: Pydantic 2.9+
- **Testing**: Pytest
- **Package Management**: UV

### Application Structure

```
backend/app/
├── main.py           # Application entry point
├── models.py         # Pydantic models & enums
├── data.py           # Data storage & queries
└── routers/          # Endpoint handlers
    ├── animals.py    # Animal CRUD operations
    └── stats.py      # Statistics aggregation
```

### Key Design Patterns

#### 1. **Dependency Injection**
FastAPI's dependency injection system is used implicitly through router organization.

#### 2. **Data Access Layer**
`data.py` provides a clean interface for data operations:
- `get_all_animals(filters)` - Query with filters
- `get_animal_by_id(id)` - Single record retrieval
- `search_animals(query)` - Full-text search
- `get_stats()` - Aggregation queries

#### 3. **Type Safety**
Pydantic models ensure type safety throughout:
```python
class Animal(BaseModel):
    id: int
    name: str
    species: str
    animal_class: AnimalClass  # Enum validation
    # ... more fields
```

#### 4. **Router Organization**
Endpoints are logically grouped by resource:
- `/api/animals/*` - Animal operations
- `/api/stats` - Statistics

### Data Model

#### Enums
- `AnimalClass`: Mammal, Bird, Reptile, Amphibian, Fish, Invertebrate
- `Diet`: Carnivore, Herbivore, Omnivore
- `ConservationStatus`: Least Concern, Vulnerable, Endangered, Critically Endangered

#### Main Model: Animal
```python
{
    "id": 1,
    "name": "African Elephant",
    "species": "Loxodonta africana",
    "animal_class": "Mammal",
    "habitat": "African savannas and forests",
    "diet": "Herbivore",
    "lifespan": "60-70 years",
    "behavior": "Social, lives in matriarchal herds",
    "size": "3-4 meters tall",
    "weight": "4,000-7,000 kg",
    "speed": "40 km/h",
    "color": "Gray",
    "interesting_fact": "...",
    "conservation_status": "Endangered"
}
```

### API Design

#### RESTful Principles
- **Resources**: Animals are the primary resource
- **HTTP Methods**: GET for read operations (no mutations in this demo)
- **Status Codes**: 200 (success), 404 (not found), 500 (server error)
- **JSON**: All responses use JSON format

#### Endpoints

1. **List Animals**
   ```
   GET /api/animals?animal_class=Mammal&habitat=forest
   Response: Array of Animal objects
   ```

2. **Get Animal**
   ```
   GET /api/animals/1
   Response: Single Animal object or 404
   ```

3. **Search**
   ```
   GET /api/animals/search?q=tiger
   Response: Array of matching Animals
   ```

4. **Statistics**
   ```
   GET /api/stats
   Response: AnimalStats object with aggregations
   ```

### CORS Configuration
```python
allow_origins=[
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # Create React App fallback
]
```

### Testing Strategy

#### Test Coverage
- **Model Tests**: Validation, enums, optional fields
- **API Tests**: All endpoints, filters, error cases
- **17 Total Tests**: 100% endpoint coverage

#### Test Organization
```python
# Model validation
test_valid_animal()
test_invalid_animal_class()

# API functionality
test_list_all_animals()
test_filter_by_class()
test_search_animals()
test_get_stats()
```

## Frontend Architecture

### Technology Stack
- **Framework**: React 18.3
- **Build Tool**: Vite 5.4
- **Styling**: CSS3 (no framework)
- **State**: React Hooks (useState, useEffect)
- **HTTP**: Native Fetch API

### Application Structure

```
frontend/src/
├── App.jsx                # Root component
├── components/            # Feature components
│   ├── AnimalCard.jsx
│   ├── AnimalGrid.jsx
│   ├── AnimalDetail.jsx
│   ├── SearchBar.jsx
│   └── StatsPanel.jsx
└── services/
    └── api.js             # API client
```

### Component Hierarchy

```
App
├── Header (static)
├── Nav (view toggle)
├── Main
│   ├── [Grid View]
│   │   ├── SearchBar
│   │   └── AnimalGrid
│   │       └── AnimalCard (×N)
│   └── [Stats View]
│       └── StatsPanel
├── AnimalDetail (modal)
└── Footer (static)
```

### State Management

#### Application State (App.jsx)
```javascript
const [animals, setAnimals] = useState([])
const [stats, setStats] = useState(null)
const [selectedAnimal, setSelectedAnimal] = useState(null)
const [loading, setLoading] = useState(true)
const [error, setError] = useState(null)
const [view, setView] = useState('grid')
const [filters, setFilters] = useState({...})
```

#### State Flow
1. **Initial Load**: Fetch all animals + stats
2. **Filter Change**: Re-fetch with filters
3. **Search**: Replace animals with search results
4. **View Toggle**: Switch between grid/stats
5. **Animal Select**: Open detail modal

### Data Flow

```
User Action → Event Handler → API Call → State Update → Re-render

Example: Search Flow
─────────────────────
1. User types "tiger" and submits
2. handleSearch(query) called
3. api.searchAnimals(query) makes HTTP request
4. Response updates animals state
5. AnimalGrid re-renders with results
```

### API Client Design

Singleton pattern with async methods:
```javascript
class AnimalAPI {
  async getAllAnimals(filters) { ... }
  async getAnimalById(id) { ... }
  async searchAnimals(query) { ... }
  async getStats() { ... }
}

export default new AnimalAPI()
```

Benefits:
- Centralized API configuration
- Consistent error handling
- Easy to mock for testing

### Component Design Patterns

#### 1. **Presentational Components**
Pure components that receive props and render UI:
- `AnimalCard`: Displays animal data
- `AnimalGrid`: Layout container
- `StatsPanel`: Visualizes statistics

#### 2. **Container Components**
Manage state and logic:
- `App`: Application state and orchestration
- `SearchBar`: Form state and input handling

#### 3. **Modal Pattern**
`AnimalDetail` uses overlay pattern:
```jsx
<div className="overlay" onClick={onClose}>
  <div className="modal" onClick={e => e.stopPropagation()}>
    {/* Content */}
  </div>
</div>
```

### Styling Architecture

#### CSS Organization
- **Component-scoped**: Each component has its own CSS file
- **BEM-like naming**: `.component-name__element`
- **No CSS-in-JS**: Plain CSS for simplicity

#### Layout Techniques
- **Flexbox**: Navigation, card internals
- **Grid**: Animal grid, info grids
- **Media Queries**: Responsive breakpoints

#### Color System
```css
/* Primary */
--primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Conservation Status */
--least-concern: #4CAF50;
--vulnerable: #FF9800;
--endangered: #F44336;
--critically-endangered: #B71C1C;
```

### Performance Considerations

#### 1. **No Over-fetching**
- Fetch all animals once on load
- Filters/search return subsets efficiently

#### 2. **Component Optimization**
- React.StrictMode for development warnings
- No unnecessary re-renders (stable callbacks)

#### 3. **Code Splitting**
Vite automatically splits code for production builds

## Communication Protocol

### Request/Response Flow

#### List Animals with Filter
```
Client                          Server
  │                               │
  │  GET /api/animals?class=Mammal
  ├──────────────────────────────>│
  │                               │
  │         200 OK                │
  │         [Array of Animals]    │
  │<────────────────────────────┤
  │                               │
```

#### Search
```
Client                          Server
  │                               │
  │  GET /api/animals/search?q=tiger
  ├──────────────────────────────>│
  │                               │
  │         200 OK                │
  │         [Matching Animals]    │
  │<────────────────────────────┤
  │                               │
```

#### Error Handling
```
Client                          Server
  │                               │
  │  GET /api/animals/999         │
  ├──────────────────────────────>│
  │                               │
  │         404 Not Found         │
  │         {"detail": "..."}     │
  │<────────────────────────────┤
  │                               │
```

### Data Formats

#### Animals Array
```json
[
  {
    "id": 1,
    "name": "African Elephant",
    "species": "Loxodonta africana",
    ...
  },
  ...
]
```

#### Statistics
```json
{
  "total_animals": 10,
  "by_class": {
    "Mammal": 4,
    "Bird": 2,
    ...
  },
  "by_diet": {...},
  "by_habitat": {...},
  "by_conservation_status": {...}
}
```

## Development Workflow

### Local Development
```bash
# Terminal 1: Backend
cd backend
uv run uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Hot Reload
- **Backend**: Uvicorn watches Python files
- **Frontend**: Vite HMR for instant updates

### Testing Workflow
```bash
# Run tests
cd backend
uv run pytest -v

# Test with coverage
uv run pytest --cov=app

# Test specific file
uv run pytest tests/test_api.py -v
```

## Deployment Considerations

### Backend Deployment
```bash
# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000

# With workers (production)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend Deployment
```bash
# Build
npm run build

# Output: dist/ directory
# Deploy to: Netlify, Vercel, S3, etc.
```

### Environment Variables
```bash
# Backend
export API_PORT=8000

# Frontend (update api.js)
export VITE_API_URL=https://api.example.com
```

## Security Considerations

### Current State (Development)
- No authentication/authorization
- CORS open to localhost
- No rate limiting
- No input sanitization beyond Pydantic

### Production Recommendations
1. **Authentication**: Add JWT tokens
2. **CORS**: Restrict to production domain
3. **Rate Limiting**: Prevent abuse
4. **Input Validation**: Additional checks beyond Pydantic
5. **HTTPS**: Encrypt traffic
6. **CSP**: Content Security Policy headers

## Scalability Considerations

### Current Limitations
- In-memory data (no persistence)
- No pagination
- Single-threaded server
- No caching

### Scaling Path
1. **Database**: PostgreSQL/MongoDB
2. **Caching**: Redis for stats
3. **Pagination**: Limit results
4. **CDN**: Static assets
5. **Load Balancing**: Multiple backend instances

## Future Enhancements

### Backend
- [ ] Database integration (SQLAlchemy)
- [ ] Authentication system
- [ ] Image upload/storage
- [ ] Admin API
- [ ] WebSocket support for real-time updates

### Frontend
- [ ] Image gallery
- [ ] Advanced filtering (multi-select, ranges)
- [ ] Animal comparison
- [ ] Favorites (localStorage)
- [ ] Dark mode
- [ ] Accessibility improvements
- [ ] Internationalization (i18n)

## Lessons Learned

### What Works Well
- Pydantic validation catches errors early
- FastAPI automatic docs are invaluable
- React functional components are simple
- Vite build speeds are excellent

### Trade-offs Made
- Hard-coded data vs. database (simplicity vs. persistence)
- No state management library (simple vs. scalable)
- CSS files vs. CSS-in-JS (traditional vs. modern)
- No TypeScript (faster development vs. type safety)

## References

- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- Vite: https://vitejs.dev/
- Pydantic: https://docs.pydantic.dev/
- UV: https://docs.astral.sh/uv/
