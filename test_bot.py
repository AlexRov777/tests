import pytest
from unittest.mock import AsyncMock, patch
from bot import get_weather, weather, recommend_hairstyle, button, buy, color_sovet
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

@pytest.mark.asyncio
async def test_get_weather_success():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {
            "cod": "200",
            "main": {"temp": 25},
            "weather": [{"description": "ясно"}]
        }
        temp, description = get_weather("Москва")
        assert temp == 25
        assert description == "ясно"

@pytest.mark.asyncio
async def test_get_weather_not_found():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {
            "cod": "404"
        }
        temp, description = get_weather("Неверный_город")
        assert temp is None
        assert description is None

@pytest.mark.asyncio
async def test_weather_command_no_city():
    mock_update = AsyncMock()
    mock_context = AsyncMock()
    mock_context.args = []
    await weather(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once_with(
        "Ах, как же я могу творить стильные чудеса, если не знаю, где вы находитесь? Пожалуйста, назовите город, и я тут же к вашим услугам!"
    )

@pytest.mark.asyncio
async def test_recommend_hairstyle():
    mock_update = AsyncMock()
    mock_context = AsyncMock()
    await recommend_hairstyle(mock_update, mock_context)
    keyboard = [
        [InlineKeyboardButton("Круглая", callback_data='круглая')],
        [InlineKeyboardButton("Овальная", callback_data='овальная')],
        [InlineKeyboardButton("Квадратная", callback_data='квадратная')],
        [InlineKeyboardButton("Треугольная", callback_data='треугольная')],
        [InlineKeyboardButton("Ромбовидная", callback_data='ромбовидная')]
    ]
    mock_update.message.reply_text.assert_called_once_with(
        "Выберите свою форму лица, дорогуша, и я мигом расскажу вам, как стать настоящей иконой стиля:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

@pytest.mark.asyncio
async def test_button_callback():
    mock_update = AsyncMock()
    mock_context = AsyncMock()
    mock_update.callback_query.data = 'круглая'
    await button(mock_update, mock_context)
    mock_update.callback_query.answer.assert_called_once()
    mock_update.callback_query.edit_message_text.assert_called_once_with(
        text="Рекомендации для вашей прекрасной формы лица:\n"
             "Ах, круглая форма лица! Я бы предложил вам асимметричные стрижки — удлинённый боб или каскад! Немного дерзости, немного стиля, и вы будете блистать!"
    )

@pytest.mark.asyncio
async def test_color_sovet_success():
    mock_update = AsyncMock()
    mock_context = AsyncMock()
    mock_context.args = ["красный"]
    await color_sovet(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once_with(
        "Красный просто идеально сочетается с белым, чёрным, серым или даже золотым — восхитительная игра контрастов, дорогая!"
    )

@pytest.mark.asyncio
async def test_color_sovet_no_color():
    mock_update = AsyncMock()
    mock_context = AsyncMock()
    mock_context.args = []
    await color_sovet(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once_with(
        "О, дорогуша, укажите цвет, и я тут же расскажу, как с ним играть!"
    )

@pytest.mark.asyncio
async def test_buy_success():
    mock_update = AsyncMock()
    mock_context = AsyncMock()
    mock_context.args = ["платье"]
    await buy(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once()

@pytest.mark.asyncio
async def test_buy_no_search_query():
    mock_update = AsyncMock()
    mock_context = AsyncMock()
    mock_context.args = []
    await buy(mock_update, mock_context)
    mock_update.message.reply_text.assert_called_once_with(
        "Ах, ну конечно, укажите, что именно ищете, и я тут же найду для вас лучшее!"
    )


