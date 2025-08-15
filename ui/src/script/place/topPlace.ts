import {
  getTopPlaces,
  type TopPlaceRating,
} from '../../services/place/tw-top-places';

export function topPlaces() {
  return {
    places: [] as TopPlaceRating[],
    loading: false,
    error: '',
    async fetch() {
      this.loading = true;
      this.error = '';
      try {
        const result = await getTopPlaces();
        if (result.success && result.data && result.data.places) {
          this.places = result.data.places;
        } else {
          this.error = result.message || 'Gagal memuat data';
        }
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
      } catch (e) {
        this.error = 'Terjadi kesalahan saat mengambil data';
      } finally {
        this.loading = false;
      }
    },
    init() {
      this.fetch();
    },
  };
}
