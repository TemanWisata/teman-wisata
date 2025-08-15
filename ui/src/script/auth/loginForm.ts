import { loginUser } from '../../services/auth/tw-login';

export function loginForm() {
  return {
    show: false,
    success: null as boolean | null,
    username: '',
    password: '',
    message: '',
    async submit() {
      this.message = '';
      try {
        const result = await loginUser({
          username: this.username,
          password: this.password,
        });
        if (result.success) {
          this.success = true;
          this.message = 'Login successful!';
          window.location.href = '/recommender.html';
        } else {
          this.success = false;
          this.message = result.message || 'Login failed';
        }
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
      } catch (e) {
        this.message = 'An error occurred';
      }
    },
  };
}
