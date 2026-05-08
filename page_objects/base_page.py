from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import allure


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    @allure.step('Подождать прогрузки элемента')
    def wait_visibility_of_element(self, locator):
        WebDriverWait(self.driver, 10).until(expected_conditions.visibility_of_element_located(locator))

    @allure.step('Найти элемент на странице')
    def find_element_with_wait(self, locator):
        self.wait_visibility_of_element(locator)
        return self.driver.find_element(*locator)

    @allure.step('Кликнуть на элемент')
    def click_on_element(self, locator):
        target = self.check_element_is_clickable(locator)
        click = ActionChains(self.driver)
        click.move_to_element(target).click().perform()

    @allure.step('Ввести значение в поле ввода')
    def send_keys_to_input(self, locator, keys):
        self.driver.find_element(*locator).send_keys(keys)

    @allure.step('Перетащить элемент')
    def drag_and_drop_element(self, source_element, target_element):
        self.driver.execute_script("""
            function simulateDragDrop(sourceNode, destinationNode) {
                var EVENT_TYPES = {
                    DRAG_END: 'dragend',
                    DRAG_START: 'dragstart',
                    DROP: 'drop'
                };
                function customEvent(typeOfEvent) {
                    var event = document.createEvent('CustomEvent');
                    event.initCustomEvent(typeOfEvent, true, true, null);
                    event.dataTransfer = {
                        data: {},
                        setData: function(type, val) { this.data[type] = val; },
                        getData: function(type) { return this.data[type]; }
                    };
                    return event;
                }
                function dispatchEvent(node, typeOfEvent) {
                    var event = customEvent(typeOfEvent);
                    node.dispatchEvent(event);
                }
                dispatchEvent(sourceNode, EVENT_TYPES.DRAG_START);
                dispatchEvent(destinationNode, EVENT_TYPES.DROP);
                dispatchEvent(sourceNode, EVENT_TYPES.DRAG_END);
            }
            simulateDragDrop(arguments[0], arguments[1]);
        """, source_element, target_element)

    @allure.step('Получить текст на элементе')
    def get_text_on_element(self, locator):
        self.wait_visibility_of_element(locator)
        return self.driver.find_element(*locator).text

    @allure.step('Проверить отображение элемента')
    def check_displaying_of_element(self, locator):
        return self.driver.find_element(*locator).is_displayed()

    @allure.step('Подождать, пока элемент закроется')
    def wait_for_closing_of_element(self, locator):
        WebDriverWait(self.driver, 15).until_not(expected_conditions.visibility_of_element_located(locator))

    @allure.step('Проверить кликабельность элемента')
    def check_element_is_clickable(self, locator):
        return WebDriverWait(self.driver, 15).until(expected_conditions.element_to_be_clickable(locator))

    @allure.step('Подождать смену текста на элементе')
    def wait_for_element_to_change_text(self, locator, value):
        return WebDriverWait(self.driver, 10).until_not(expected_conditions.
                                                        text_to_be_present_in_element(locator, value))