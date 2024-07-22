import subprocess
import json

# Function to call the Node.js module
def google_correction(query):

    result = subprocess.run(
        ['node', '-e', f"""
        const google = require('googlethis');
        (async () => {{
            const options = {{
                page: 0,
                safe: false,
                parse_ads: false,
                additional_params: {{
                    hl: 'en'
                }}
            }};
            const response = await google.search('{query}', options);
            console.log(JSON.stringify(response));
        }})();
        """],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        response = json.loads(result.stdout)
        corrected_response = response['did_you_mean']
        print("corrected_response:", corrected_response)

        if corrected_response is None:
            return query
        return corrected_response
    else:
        print('Error:', result.stderr)
        return None

