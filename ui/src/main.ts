import './style.css';
import 'htmx.org';
import Alpine from 'alpinejs';
import { loginForm, topPlaces, placeDetail, placeRatingAlpine } from './script';

declare global {
  interface Window {
    Alpine: typeof Alpine;
    loginForm: typeof loginForm;
    topPlaces: typeof topPlaces;
    placeDetail: typeof placeDetail;
    placeRatingAlpine: typeof placeRatingAlpine;
  }
}
window.Alpine = Alpine;
window.loginForm = loginForm;
window.topPlaces = topPlaces;
window.placeDetail = placeDetail;
window.placeRatingAlpine = placeRatingAlpine;
Alpine.start();
