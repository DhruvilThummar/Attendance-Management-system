/**
 * Main Application Entry Point
 */
import { initPasswordToggles, initCapsLockWarning, initAutoDismiss } from './modules/ui.js';
import { initFormValidation } from './modules/validation.js';

document.addEventListener("DOMContentLoaded", () => {
    console.log("Attendify Modular JS Loaded");

    initPasswordToggles();
    initCapsLockWarning();
    initAutoDismiss();
    initFormValidation();
});
