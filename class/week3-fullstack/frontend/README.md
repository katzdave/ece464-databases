# Animal Explorer Frontend

React + Vite frontend for the Animal Explorer application.

## Features

- **Grid View**: Browse animals in a responsive card grid
- **Detail Modal**: Click any animal for comprehensive information
- **Search**: Find animals by name, species, or facts
- **Filters**: Filter by animal class or habitat
- **Statistics Dashboard**: Visual data about the collection
- **Responsive Design**: Mobile-friendly layout

## Tech Stack

- React 18.3
- Vite 5.4 (build tool)
- CSS3 (Flexbox & Grid)
- Fetch API for HTTP requests

## Setup

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── App.jsx              # Main application component
│   ├── App.css              # Global app styles
│   ├── main.jsx             # React entry point
│   ├── index.css            # Base styles
│   ├── components/          # React components
│   │   ├── AnimalCard.jsx   # Individual animal card
│   │   ├── AnimalGrid.jsx   # Grid layout container
│   │   ├── AnimalDetail.jsx # Detail modal
│   │   ├── SearchBar.jsx    # Search & filter UI
│   │   └── StatsPanel.jsx   # Statistics dashboard
│   └── services/
│       └── api.js           # API client
├── index.html               # HTML entry point
├── vite.config.js           # Vite configuration
└── package.json             # Dependencies
```

## Components

### App.jsx
Main component managing application state and routing between views.

**State**:
- `animals`: Current list of animals to display
- `stats`: Statistics data
- `selectedAnimal`: Animal to show in detail modal
- `loading`: Loading state
- `error`: Error message
- `view`: Current view ('grid' or 'stats')
- `filters`: Active filters

**Key Functions**:
- `loadAnimals()`: Fetch animals from API
- `loadStats()`: Fetch statistics
- `handleSearch()`: Execute search query
- `handleFilterChange()`: Apply filters

### AnimalCard.jsx
Displays a single animal in card format.

**Props**:
- `animal`: Animal object
- `onSelect`: Callback when card is clicked

### AnimalGrid.jsx
Grid layout for animal cards with loading/error states.

**Props**:
- `animals`: Array of animal objects
- `onAnimalSelect`: Callback when an animal is clicked
- `loading`: Boolean loading state
- `error`: Error message string

### AnimalDetail.jsx
Modal overlay showing detailed animal information.

**Props**:
- `animal`: Animal object to display
- `onClose`: Callback to close modal

**Sections**:
- General Information (habitat, diet, lifespan, behavior)
- Physical Characteristics (size, weight, speed, color)
- Fun Fact (interesting fact)
- Conservation Status (with color coding)

### SearchBar.jsx
Search input and filter controls.

**Props**:
- `onSearch`: Callback for search queries
- `onFilterChange`: Callback when filters change
- `filters`: Current filter values

**Features**:
- Text search input
- Animal class dropdown
- Habitat text filter
- Clear button

### StatsPanel.jsx
Statistics dashboard with visual charts.

**Props**:
- `stats`: Statistics object from API

**Displays**:
- Total animal count
- Distribution by class (bar chart)
- Distribution by diet (bar chart)
- Conservation status (color-coded bar chart)

## API Client (services/api.js)

Handles all backend communication.

**Methods**:
- `getAllAnimals(filters)`: Get all animals with optional filters
- `getAnimalById(id)`: Get single animal
- `searchAnimals(query)`: Search animals
- `getStats()`: Get statistics

**Configuration**:
- Base URL: `http://localhost:8000`
- Change this if backend runs on a different port

## Styling

Each component has its own CSS file following BEM-like conventions:
- `component-name`: Block
- `component-name__element`: Element
- `component-name--modifier`: Modifier

**Color Scheme**:
- Primary: Purple gradient (#667eea to #764ba2)
- Success: Green (#4CAF50)
- Warning: Orange (#FF9800)
- Error: Red (#F44336)
- Neutral: Gray shades

**Conservation Status Colors**:
- Least Concern: Green (#4CAF50)
- Vulnerable: Orange (#FF9800)
- Endangered: Red (#F44336)
- Critically Endangered: Dark Red (#B71C1C)

## Development

### Hot Module Replacement
Vite provides instant HMR - changes appear immediately without full page reload.

### Browser DevTools
Use React DevTools extension for component inspection.

### API Testing
Backend must be running at http://localhost:8000 for the app to work.

### Common Issues

**CORS Errors**: Ensure backend CORS is configured for http://localhost:5173

**API Connection Failed**: Check that backend is running

**Blank Page**: Check browser console for errors

## Building for Production

```bash
npm run build
```

Creates optimized bundle in `dist/` directory.

To preview:
```bash
npm run preview
```

## Future Enhancements

Potential additions:
- Animal images
- Pagination for large datasets
- Favorites with localStorage
- Dark mode toggle
- Comparison feature
- Quiz/game mode
- Social sharing
- Export data (CSV/JSON)
