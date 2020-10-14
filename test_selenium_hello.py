"""Perform a Google search using Selenium and a headless Chrome browser."""
import selenium
import selenium.webdriver


def test_selenium_hello():
    """Perform a Google search using Selenium and a headless Chrome browser."""

    # Configure Selenium
    #
    # Pro-tip: remove the "headless" option and set a breakpoint.  A Chrome
    # browser window will open, and you can play with it using the developer
    # console.
    options = selenium.webdriver.chrome.options.Options()
    options.add_argument("headless")
    driver = selenium.webdriver.Chrome(options=options)

    # An implicit wait tells WebDriver to poll the DOM for a certain amount of
    # time when trying to find any element (or elements) not immediately
    # available. Once set, the implicit wait lasts for the life of the
    # WebDriver object.
    #
    # https://selenium-python.readthedocs.io/waits.html#implicit-waits
    driver.implicitly_wait(1)

    # Load Google search main page
    driver.get("https://www.google.com")

    # Find the search input box, which looks like this:
    #   <input name="q" type="text">
    input_element = driver.find_element_by_xpath("//input[@name='q']")

    # Type "hello world" into the search box and click submit
    input_element.send_keys("hello world")
    input_element.submit()

    # Find the search results, which look something like this:
    #   <div class="g">
    #     <div class="r">
    #       <a href="https://en.wikipedia.org/wiki/%22Hello,_World!%22_program">
    #         <h3>
    #           "Hello, World!" program - Wikipedia
    #         </h3>
    #       </a>
    #     </div>
    #   </div>
    results = driver.find_elements_by_xpath('//div[@class="g"]//a//h3')

    # Print search results, ignoring non-standard search results which lack
    # text, like "Videos" or "People also ask".
    for result in results:
        if result.text:
            print(result.text)

    # Cleanup
    driver.quit()


if __name__ == "__main__":
    test_selenium_hello()
