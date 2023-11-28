import React from 'react';
import './CodeBlock.css';

import CodeMirror from '@uiw/react-codemirror';
import { javascript } from '@codemirror/lang-javascript';
import { python } from '@codemirror/lang-python';
import { css } from '@codemirror/lang-css';
import { html } from '@codemirror/lang-html';
import { andromeda } from '@uiw/codemirror-theme-andromeda';
import { monokai } from '@uiw/codemirror-theme-monokai';

function CodeBlock({ codevalue, language}) {

  const extensionsMap = {
    'python': python(),
    'javascript': javascript(),
    'css': css(),
    'html': html(),
    // add other languages here
  };

  // Fallback to javascript if the language is not found in the map
  const extension = extensionsMap[language] || javascript();

  return (
    <CodeMirror 
      value={codevalue} 
      extensions={[extension]} 
      theme={monokai}
      readOnly={true}
    />
  );

}

export default CodeBlock;