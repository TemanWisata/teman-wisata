import './style.css';
import 'htmx.org';
import Alpine from 'alpinejs';
import { loginForm, topPlaces, placeDetail } from './script';

declare global {
  interface Window {
    Alpine: typeof Alpine;
    loginForm: typeof loginForm;
    topPlaces: typeof topPlaces;
    placeDetail: typeof placeDetail;
  }
}
window.Alpine = Alpine;
window.loginForm = loginForm;
window.topPlaces = topPlaces;
window.placeDetail = placeDetail;
Alpine.start();
