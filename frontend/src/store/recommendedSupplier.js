import http from '../services/http';

/**
 * Fetch recommended suppliers from the API
 * @returns {Promise} - Resolves to the array of recommended suppliers
 */
export async function fetchRecommendedSuppliers() {
  try {
    const response = await http.get('/api/recommended_suppliers/');
    return response.recommended_suppliers;
  } catch (error) {
    console.error('Failed to fetch recommended suppliers:', error);
    throw error;
  }
}

/**
 * Filter and sort suppliers based on criteria
 * @param {Array} suppliers - Array of supplier objects
 * @param {Object} filters - Filter and sort criteria
 * @returns {Array} - Filtered and sorted suppliers
 */
export function filterSuppliers(suppliers, filters) {
  return suppliers.filter(supplier => {
    // Search filter
    if (filters.search && !supplier.name.toLowerCase().includes(filters.search.toLowerCase())) {
      return false;
    }
    
    // Investment filter
    if (filters.openForInvestment && !supplier.is_open_for_investment) {
      return false;
    }
    
    // Growth rate filter
    if (filters.minGrowthRate !== null && supplier.growth_rate < filters.minGrowthRate) {
      return false;
    }
    
    return true;
  }).sort((a, b) => {
    const factor = filters.sortDirection === 'desc' ? -1 : 1;
    
    switch (filters.sortBy) {
      case 'name':
        return factor * a.name.localeCompare(b.name);
      case 'recentSales':
        return factor * (a.recent_sales - b.recent_sales);
      case 'growthRate':
        return factor * (a.growth_rate - b.growth_rate);
      case 'productsCount':
        return factor * (a.products_count - b.products_count);
      case 'score':
      default:
        return factor * (a.score - b.score);
    }
  });
}