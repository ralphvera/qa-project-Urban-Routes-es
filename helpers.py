def retrieve_phone_code(driver) -> str:
    """This code retrieves phone confirmation number and returns it as a string.
    Use it when application waits for the confirmation code to pass it into your tests.
    The phone confirmation code can only be obtained after it was requested in application."""

    import json
    import time
    from selenium.common.exceptions import WebDriverException


    code = None
    max_attempts = 20  # Increased attempts
    wait_time = 0.5  # Wait between attempts

    for i in range(max_attempts):
        try:
            # Get all performance logs
            all_logs = driver.get_log('performance')

            # Filter logs for the SMS API endpoint
            logs = [log["message"] for log in all_logs
                    if log.get("message") and 'api/v1/number?number' in log.get("message")]

            print(f"Attempt {i + 1}: Found {len(logs)} matching logs")  # Debug info

            for log in reversed(logs):
                try:
                    message_data = json.loads(log)["message"]

                    # Check if this is a response (not a request)
                    if message_data["method"] != "Network.responseReceived":
                        continue

                    request_id = message_data["params"]["requestId"]

                    # Try to get the response body
                    body = driver.execute_cdp_cmd('Network.getResponseBody',
                                                  {'requestId': request_id})

                    # Extract digits from the response
                    if body and 'body' in body:
                        code = ''.join([x for x in body['body'] if x.isdigit()])

                        if code:
                            print(f"Found code: {code}")  # Debug info
                            return code

                except (KeyError, json.JSONDecodeError, WebDriverException) as e:
                    # Log might not have the expected structure, continue
                    print(f"Error parsing log: {e}")  # Debug info
                    continue

        except WebDriverException as e:
            print(f"WebDriver exception: {e}")  # Debug info
            pass

        # Wait before next attempt
        time.sleep(wait_time)

    # If we get here, no code was found
    raise Exception(
        f"No phone confirmation code found after {max_attempts} attempts.\n"
        "Please use retrieve_phone_code only after the code was requested in your application.\n"
        "Make sure Chrome DevTools Protocol logging is enabled."
    )