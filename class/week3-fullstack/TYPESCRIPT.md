# TypeScript Integration - Type Sharing Between Frontend and Backend

## Overview

This project demonstrates **automatic type sharing** between the FastAPI backend and React frontend using OpenAPI. The backend's Pydantic models automatically generate TypeScript types for the frontend.

## How It Works

```
Backend (Python)          OpenAPI Schema          Frontend (TypeScript)
─────────────────         ──────────────          ────────────────────

Pydantic Models    →     /openapi.json     →     Generated Types
  - Animal                                          - Animal
  - AnimalStats                                     - AnimalStats
  - Enums                                           - Enums
```

### 1. Backend Generates OpenAPI Schema

FastAPI automatically generates an OpenAPI 3.0 schema from your Pydantic models:

**Backend (`backend/app/models.py`)**:
```python
class Animal(BaseModel):
    id: int
    name: str
    species: str
    animal_class: AnimalClass  # Enum
    # ... more fields
```

**Generated OpenAPI**: http://localhost:8888/openapi.json

### 2. Frontend Generates TypeScript Types

Using `openapi-typescript`, we generate TypeScript types from the OpenAPI schema:

```bash
npm run generate-types
```

This creates `src/types/api.ts` with all types from the backend.

### 3. Use Shared Types in Frontend

**Frontend (`src/services/api.ts`)**:
```typescript
import type { Animal, AnimalStats } from '../types';

class AnimalAPI {
  async getAllAnimals(filters = {}): Promise<Animal[]> {
    // TypeScript knows the exact shape of Animal!
  }
}
```

## Setup Instructions

### Initial Setup (Already Done)

1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install --save-dev typescript @types/react @types/react-dom openapi-typescript
   ```

2. **Create TypeScript Config**:
   - `tsconfig.json` - Main TypeScript configuration
   - `tsconfig.node.json` - Node/Vite configuration

3. **Generate Types**:
   ```bash
   npm run generate-types
   ```

### Workflow for Type Changes

When you modify backend models:

1. **Update Backend Model** (`backend/app/models.py`):
   ```python
   class Animal(BaseModel):
       new_field: str  # Add a new field
   ```

2. **Restart Backend** (if needed):
   ```bash
   cd backend
   uv run uvicorn app.main:app --reload
   ```

3. **Regenerate Frontend Types**:
   ```bash
   cd frontend
   npm run generate-types
   ```

4. **Types Automatically Update** - TypeScript will now know about the new field!

## Generated Types Structure

### `src/types/api.ts` (Auto-generated)

```typescript
export interface components {
  schemas: {
    Animal: {
      id: number;
      name: string;
      species: string;
      animal_class: "Mammal" | "Bird" | "Reptile" | ...;
      // ... all fields with exact types
    };
    AnimalStats: {
      total_animals: number;
      by_class: { [key: string]: number };
      // ...
    };
  };
}

export interface paths {
  "/api/animals": {
    get: operations["list_animals_api_animals_get"];
  };
  // ... all API endpoints
}
```

### `src/types/index.ts` (Custom exports)

```typescript
// Extract commonly used types for easier imports
export type Animal = components['schemas']['Animal'];
export type AnimalStats = components['schemas']['AnimalStats'];
export type AnimalClass = components['schemas']['AnimalClass'];
// ...
```

## Benefits

### 1. **Type Safety**

```typescript
// ✅ TypeScript catches errors at compile time
const animal: Animal = {
  id: 1,
  name: "Lion",
  // ❌ Error: missing required field 'species'
};
```

### 2. **Autocomplete**

Your IDE provides intelligent autocomplete based on backend models:

```typescript
api.getAllAnimals().then(animals => {
  animals[0]. // IDE shows: id, name, species, animal_class, ...
});
```

### 3. **Refactoring Safety**

If you rename a field in the backend:
- Regenerate types
- TypeScript shows all places that need updating
- No runtime errors!

### 4. **Documentation**

Types serve as documentation:

```typescript
// Hover over Animal to see all fields and their types
const handleAnimal = (animal: Animal) => {
  // ...
};
```

## File Structure

```
frontend/
├── src/
│   ├── types/
│   │   ├── api.ts          # ⚙️ Auto-generated from OpenAPI
│   │   └── index.ts        # 📝 Custom type exports
│   ├── services/
│   │   └── api.ts          # 🔌 API client with types
│   ├── App.tsx             # 📱 Main app with types
│   └── main.tsx
├── tsconfig.json
├── tsconfig.node.json
└── package.json
```

## NPM Scripts

```json
{
  "scripts": {
    "dev": "vite",                    // Start dev server
    "build": "tsc && vite build",     // Type-check + build
    "type-check": "tsc --noEmit",     // Check types only
    "generate-types": "openapi-typescript http://localhost:8888/openapi.json -o src/types/api.ts"
  }
}
```

## Example: Using Shared Types

### API Client (`src/services/api.ts`)

```typescript
import type { Animal, AnimalStats, AnimalFilters } from '../types';

class AnimalAPI {
  // Return type is automatically validated
  async getAllAnimals(filters: AnimalFilters = {}): Promise<Animal[]> {
    const response = await fetch(`${API_BASE_URL}/api/animals`);
    return await response.json(); // TypeScript knows this is Animal[]
  }

  async getStats(): Promise<AnimalStats> {
    const response = await fetch(`${API_BASE_URL}/api/stats`);
    return await response.json(); // TypeScript knows this is AnimalStats
  }
}
```

### React Component (`src/App.tsx`)

```typescript
import type { Animal, AnimalStats } from './types';

function App() {
  // State is properly typed
  const [animals, setAnimals] = useState<Animal[]>([]);
  const [stats, setStats] = useState<AnimalStats | null>(null);
  const [selectedAnimal, setSelectedAnimal] = useState<Animal | null>(null);

  // Functions have type-safe parameters
  const handleAnimalSelect = (animal: Animal): void => {
    setSelectedAnimal(animal);
  };

  return (
    <AnimalDetail
      animal={selectedAnimal}  // Type-checked!
      onClose={handleCloseDetail}
    />
  );
}
```

## Alternative Approaches

### 1. **openapi-typescript** (Current - Simplest)
- ✅ Lightweight
- ✅ Just types, no runtime code
- ✅ Works with any HTTP client
- ❌ Manual regeneration needed

### 2. **openapi-typescript-codegen**
- Generates full API client with methods
- More code generation
- Opinionated structure

### 3. **orval**
- Generates React Query hooks
- More features
- Heavier dependency

### 4. **Manual Type Definitions**
- ❌ Duplicates backend types
- ❌ Can get out of sync
- ❌ Not recommended

## Common Issues

### Issue: Types out of sync

**Solution**: Regenerate types
```bash
npm run generate-types
```

### Issue: TypeScript errors in JSX components

**Solution**: Either:
1. Convert components to `.tsx` (recommended)
2. Create `.d.ts` declaration files
3. Add `// @ts-ignore` comments (not recommended)

### Issue: Backend not running

**Solution**: Start backend first
```bash
cd backend
uv run uvicorn app.main:app --reload
```

Then regenerate types.

## Best Practices

### 1. **Regenerate After Backend Changes**

Add to your workflow:
```bash
# Make backend changes
cd backend
# ... edit models.py ...

# Regenerate frontend types
cd ../frontend
npm run generate-types

# Type check
npm run type-check
```

### 2. **Use Strict TypeScript**

`tsconfig.json`:
```json
{
  "compilerOptions": {
    "strict": true,  // Enable all strict checks
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

### 3. **Type Your React Components**

```typescript
interface AnimalCardProps {
  animal: Animal;
  onSelect: (animal: Animal) => void;
}

function AnimalCard({ animal, onSelect }: AnimalCardProps) {
  // ...
}
```

### 4. **Use Discriminated Unions**

For view states:
```typescript
type View = 'grid' | 'stats';  // Not just string!
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Type Check
on: [push]
jobs:
  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npm install
      - run: npm run type-check  # Fails if types don't match
```

## Further Reading

- [FastAPI OpenAPI](https://fastapi.tiangolo.com/advanced/extending-openapi/)
- [openapi-typescript](https://github.com/drwpow/openapi-typescript)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)

## Summary

✅ **Single Source of Truth**: Backend Pydantic models
✅ **Automatic Type Generation**: Via OpenAPI
✅ **Type Safety**: Catch errors at compile time
✅ **Great DX**: Autocomplete and refactoring
✅ **No Duplication**: Don't maintain types twice

This approach scales from small projects to large enterprise applications!
