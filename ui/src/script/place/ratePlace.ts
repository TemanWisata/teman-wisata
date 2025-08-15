import type {
  UserRatingRequest,
  RatingResponse,
} from '../../services/place/tw-rating';

export function placeRatingAlpine(placeId: number) {
  console.log('Initializing placeRatingAlpine with placeId:', placeId);
  return {
    userRating: 0,
    loading: false,
    error: '',
    success: '',
    async submitRating() {
      this.loading = true;
      this.error = '';
      this.success = '';
      const access_token = localStorage.getItem('access_token');
      if (!access_token) {
        this.error = 'Anda belum login.';
        this.loading = false;
        return;
      }
      const payload: UserRatingRequest = {
        place_id: placeId,
        rating: this.userRating,
      };
      try {
        const response: RatingResponse = await import(
          '../../services/place/tw-rating'
        ).then((mod) => mod.ratePlace(payload, access_token!));
        if (response.success) {
          this.success = 'Rating berhasil dikirim!';
        } else {
          this.error = response.message;
        }
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
      } catch (e) {
        this.error = 'Terjadi kesalahan saat mengirim rating.';
      }
      this.loading = false;
    },
    async fetchUserRating() {
      const access_token = localStorage.getItem('access_token');
      if (!access_token) return;
      try {
        const response: RatingResponse = await import(
          '../../services/place/tw-rating'
        ).then((mod) => mod.getUserRating(placeId, access_token!));
        if (response.success && response.data) {
          this.userRating = response.data.rating;
        }
      } catch {
        // ignore error
      }
    },
    init() {
      this.fetchUserRating();
    },
  };
}
