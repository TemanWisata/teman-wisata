import { getPlaceById, type Place } from '../../services/place/tw-place';
let initialized = false;
export function placeDetail() {
  return {
    place: null as Place | null,
    loading: false,
    error: '',
    async fetch() {
      this.loading = true;
      this.error = '';
      const params = new URLSearchParams(window.location.search);
      const id = params.get('id');
      if (!id) {
        this.error = 'ID tempat tidak ditemukan di URL';
        this.loading = false;
        return;
      }
      try {
        const result = await getPlaceById(id);
        if (result.success && result.data) {
          this.place = result.data;
        } else {
          this.error = result.message || 'Gagal memuat data tempat';
        }
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
      } catch (e) {
        this.error = 'Terjadi kesalahan saat mengambil data tempat';
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
