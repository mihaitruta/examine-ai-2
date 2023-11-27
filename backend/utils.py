import re
import tiktoken

# in $ / 1K tokens
api_details = {
    'gpt-3.5-turbo-1106' : {'prompt' : 0.001, 'output' : 0.002, 'context' : 16385},
    'gpt-3.5-turbo-0613' : {'prompt' : 0.001, 'output' : 0.002, 'context' : 4096},
    'gpt-3.5-turbo-16k-1106' : {'prompt' : 0.002, 'output' : 0.004, 'context' : 16385},
    'gpt-3.5-turbo-16k-0613' : {'prompt' : 0.002, 'output' : 0.004, 'context' : 16385},
    'gpt-4-0613' : {'prompt' : 0.03, 'output' : 0.06, 'context' : 8192},
    'gpt-4-32k-0613' : {'prompt' : 0.06, 'output' : 0.12, 'context' : 32768},
    'gpt-4-1106-preview' : {'prompt' : 0.01, 'output' : 0.03, 'context' : 128000},
    }

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def escape_html(text):
    """Escape special HTML characters in text."""
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\"", "&quot;")
                .replace("'", "&#039;"))

def format_message(text):
    in_code_block = False
    formatted_lines = []
    code_lines = []
    code_content = ''
    language = None


    lines = text.split('\n')
    print(lines)
    lines_ct = len(text.split('\n'))
    for idx, line in enumerate(lines):
        print('processing line: ', line)
        if line.startswith('```'):
            in_code_block = not in_code_block
            if in_code_block:
                # Extract language from the start of the code block
                language = line[3:].strip() or ""
                #line = f'<div class="code-header">{language}</div><pre>'
                #formatted_lines.append(line)
                #code_block = "<div class=\"code-header\" onclick=\"handleCodeHeaderClick(`" + code_content + "`)\">python</div><pre>" + code_content + "</pre>"
            else:
                #header_line = f'<div class="code-header" onclick="handleCodeHeaderClick(`' + code_content + '`)">{language}</div><pre>'
                header_line = f'<div class="code-container"><div class="code-header">{language}</div><pre>'
                formatted_lines.append(header_line)
                formatted_lines.extend(code_lines)
                formatted_lines.append('</pre></div>')
                code_lines = []
                code_content = ''
            continue

        if in_code_block:
            code_lines.append(escape_html(line))
            code_content += line + '\n'
        else:
            print('not in code block')
            if re.match(r"^\d+\.\s+", line):
                print('line in list')
                # Apply list formatting to lines outside code blocks
                formatted_line = re.sub(r"^(\d+\.)\s+(.*)", r"<li>\2</li>", escape_html(line))
                formatted_lines.append(formatted_line)
            else:
                print('line not in list')
                formatted_line = escape_html(line)
                #if formatted_line == '':
                #    formatted_line = '<br>'
                formatted_line += '<br>'
                formatted_lines.append(formatted_line)

        if idx == lines_ct - 1:
            if in_code_block:
                header_line = f'<div class="code-header">{language}</div><pre>'
                formatted_lines.append(header_line)
                formatted_lines.extend(code_lines)
                formatted_lines.append('</pre>')


    result = '\n'.join(formatted_lines)

    return result

