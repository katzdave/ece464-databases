// Re-export API types for easier imports
export type { components, paths } from './api';

// Extract commonly used types
import type { components } from './api';

export type Animal = components['schemas']['Animal'];
export type AnimalStats = components['schemas']['AnimalStats'];
export type AnimalClass = components['schemas']['AnimalClass'];
export type Diet = components['schemas']['Diet'];
export type ConservationStatus = components['schemas']['ConservationStatus'];

// Filters type for API requests
export interface AnimalFilters {
  animal_class?: string;
  habitat?: string;
  species?: string;
}
