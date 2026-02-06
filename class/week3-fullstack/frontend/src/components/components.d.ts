// Type declarations for JSX components not yet converted to TypeScript
// This allows TypeScript files to import them without errors

declare module './SearchBar' {
  import { FC } from 'react';
  import type { AnimalFilters } from '../types';

  interface SearchBarProps {
    onSearch: (query: string) => void;
    onFilterChange: (filters: AnimalFilters) => void;
    filters: AnimalFilters;
  }

  const SearchBar: FC<SearchBarProps>;
  export default SearchBar;
}

declare module './AnimalGrid' {
  import { FC } from 'react';
  import type { Animal } from '../types';

  interface AnimalGridProps {
    animals: Animal[];
    onAnimalSelect: (animal: Animal) => void;
    loading: boolean;
    error: string | null;
  }

  const AnimalGrid: FC<AnimalGridProps>;
  export default AnimalGrid;
}

declare module './AnimalCard' {
  import { FC } from 'react';
  import type { Animal } from '../types';

  interface AnimalCardProps {
    animal: Animal;
    onSelect: (animal: Animal) => void;
  }

  const AnimalCard: FC<AnimalCardProps>;
  export default AnimalCard;
}

declare module './AnimalDetail' {
  import { FC } from 'react';
  import type { Animal } from '../types';

  interface AnimalDetailProps {
    animal: Animal;
    onClose: () => void;
  }

  const AnimalDetail: FC<AnimalDetailProps>;
  export default AnimalDetail;
}

declare module './StatsPanel' {
  import { FC } from 'react';
  import type { AnimalStats } from '../types';

  interface StatsPanelProps {
    stats: AnimalStats | null;
  }

  const StatsPanel: FC<StatsPanelProps>;
  export default StatsPanel;
}
