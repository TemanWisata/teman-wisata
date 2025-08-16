import type {
  RecommendationResponse,
  RecommenderRequest,
  Place,
} from '../../services/recommendation/tw-recommendation';
import { getUserRecommendations } from '../../services/recommendation/tw-recommendation';
let initialized = false;
export function userRecommendationComponent() {
  return {
    recommendations: [] as Place[],
    loading: false,
    show: true,
    error: '',
    async fetchRecommendations(
      payload: RecommenderRequest = { k: 10, filter_viewed: true }
    ) {
      this.loading = true;
      this.error = '';
      try {
        const response: RecommendationResponse =
          await getUserRecommendations(payload);
        if (response.success && response.data && response.data.data) {
          if (!(response.http_status === 200)) {
            this.error = response.message || 'Failed to fetch recommendations';
            this.loading = false;
            this.show = false;
          }

          this.recommendations = response.data.data.filter(Boolean) as Place[];
        } else {
          this.error = response.message || 'Failed to fetch recommendations';
        }
      } catch {
        this.error = 'Error fetching recommendations';
      } finally {
        this.loading = false;
      }
    },
    init() {
      if (initialized) return;
      initialized = true;
      this.fetchRecommendations();
    },
  };
}
