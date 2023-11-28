import React from 'react';
import './DropdownMenu.css';

function DropdownMenu({ isVisible, onMenuItemClick }) {
  return (
    <div className="dropdown-menu" style={{ display: isVisible ? 'block' : 'none' }}>
      <div className="dropdown-item" onClick={() => onMenuItemClick('Reset Chat')}>Reset Chat</div>
      <div className="dropdown-item" onClick={() => onMenuItemClick('Settings')}>Settings</div>
      <div className="dropdown-item" onClick={() => onMenuItemClick('About')}>About</div>
      {/* More dropdown items */}
    </div>
  );
}

export default DropdownMenu;