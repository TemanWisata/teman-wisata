import './style.css';
import 'htmx.org';
import htmx from 'htmx.org';
import Alpine from 'alpinejs';


declare global {
  interface Window {
    htmx: typeof htmx;
    Alpine: typeof Alpine;
  }
}
window.htmx = htmx;
window.Alpine = Alpine;

Alpine.start();
console.log('HTMX loaded:', window.htmx);
console.log('Alpine loaded:', window.Alpine);
