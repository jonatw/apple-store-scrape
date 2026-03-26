// Tree-shaken Font Awesome — only the 8 icons we actually use
import { library, dom } from '@fortawesome/fontawesome-svg-core';
import '@fortawesome/fontawesome-svg-core/styles.css';
import {
  faSun, faMoon, faCog, faChevronDown,
  faInfoCircle, faPlaneDeparture, faShareSquare
} from '@fortawesome/free-solid-svg-icons';
import { faApple } from '@fortawesome/free-brands-svg-icons';

library.add(faSun, faMoon, faCog, faChevronDown, faInfoCircle, faPlaneDeparture, faShareSquare, faApple);

// Replace <i> tags with inline SVGs
dom.watch();
