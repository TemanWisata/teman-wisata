import './style.css';
import 'htmx.org';
import Alpine from 'alpinejs';
import { loginForm, topPlaces } from './script';

declare global {
  interface Window {
    Alpine: typeof Alpine;
    loginForm: typeof loginForm;
    topPlaces: typeof topPlaces;
  }
}
window.Alpine = Alpine;
window.loginForm = loginForm;
window.topPlaces = topPlaces;
Alpine.start();
