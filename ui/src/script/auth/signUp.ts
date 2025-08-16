import { registerUser } from '../../services/auth/tw-register';

export function signUpComponent() {
  return {
    username: '',
    password: '',
    confirm: '',
    full_name: '',
    dob: '',
    province: '',
    loading: false,
    error: '',
    success: '',
    async submit() {
      this.error = '';
      this.success = '';
      if (
        !this.username ||
        !this.password ||
        !this.confirm ||
        !this.full_name ||
        !this.dob ||
        !this.province
      ) {
        this.error = 'Semua field wajib diisi.';
        return;
      }
      if (this.password !== this.confirm) {
        this.error = 'Konfirmasi kata sandi tidak cocok.';
        return;
      }
      this.loading = true;
      try {
        const response = await registerUser({
          username: this.username,
          password: this.password,
          full_name: this.full_name,
          dob: this.dob,
          province: this.province,
        });
        if (response.success && response.http_status === 201) {
          this.success = 'Registrasi berhasil! Silakan login.';
          this.username = '';
          this.password = '';
          this.confirm = '';
          this.full_name = '';
          this.dob = '';
          this.province = '';
        } else {
          this.error = response.message || 'Registrasi gagal.';
        }
      } catch {
        this.error = 'Terjadi kesalahan saat registrasi.';
      } finally {
        this.loading = false;
      }
    },
  };
}
