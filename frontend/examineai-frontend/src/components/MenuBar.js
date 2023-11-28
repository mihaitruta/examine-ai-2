import React from 'react';
import './MenuBar.css';
import DropdownMenu from './DropdownMenu'; // Adjust import path as necessary
import DarkButtonIcon from '.././resources/dark-mode-button.svg';
import LightButtonIcon from '.././resources/light-mode-button.svg';
import MenuButtonIconDark from '.././resources/menu-button-dark.svg';
import MenuButtonIconLight from '.././resources/menu-button-light.svg';

function MenuBar({ toggleDropdown, handleMenuItemClick, toggleTheme, theme, isDropdownVisible }) {
  return (
    <div className="menu-bar">
      <div className="menu-title">
        <div className="title-text" onClick={() => window.open('https://examine.dev/', '_blank')}>
          examine|AI
        </div>
      </div>
      <button className="menu-button" onClick={toggleDropdown}>
        <img src={theme === 'dark-mode' ? MenuButtonIconDark : MenuButtonIconLight} alt="Menu" />
        <span className={`tooltip-text ${isDropdownVisible ? 'tooltip-disabled' : ''} menu`}>Menu</span>
        <div className="menu-container" >
          <DropdownMenu isVisible={isDropdownVisible} onMenuItemClick={handleMenuItemClick} />
        </div>
      </button>
      <button className="theme-button" onClick={toggleTheme}>
        <img src={theme === 'dark-mode' ? DarkButtonIcon : LightButtonIcon} alt="Toggle Theme" />
        <span className="tooltip-text theme">Theme</span>
      </button>
    </div>
  );
}

export default MenuBar;
