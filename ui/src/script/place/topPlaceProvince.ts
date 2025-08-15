import {
  getTopPlaceByProvince,
  type TopPlaceByProvince,
  type TopPlaceProvinceResponse,
} from '../../services/place/tw-top-place-province';

let initialized = false;
/**
 * Alpine.js component for displaying top places by province.
 */
export function topPlaceProvince() {
  return {
    provinces: [] as TopPlaceByProvince[],
    loading: false,
    error: '',
    async fetch() {
      this.loading = true;
      this.error = '';
      try {
        const result: TopPlaceProvinceResponse = await getTopPlaceByProvince();
        if (result.success && result.data) {
          this.provinces = result.data;
          console.log('Top places by province:', this.provinces);
        } else {
          this.error = result.message || 'Gagal memuat data';
        }
      } catch {
        this.error = 'Terjadi kesalahan saat mengambil data';
      } finally {
        this.loading = false;
      }
    },
    init() {
      if (initialized) return;
      initialized = true;
      this.fetch();
    },
  };
}
