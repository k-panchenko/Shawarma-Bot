const { Telegraf, Markup } = require('telegraf');

const bot = new Telegraf(process.env.BOT_TOKEN);

let shawaMessage = null;

bot.command('shawa', (ctx) => {
    const chatId = ctx.message.chat.id;

    if (shawaMessage) {
        ctx.reply('Кто-уже собирается пойти за шаурмой, присоединяйтесь!', {
            reply_to_message_id: shawaMessage.message_id,
        });
        return;
    }

    const options = [
        'L',
        'XL',
        'XXL',
        'Doner',
        '+ Комбо',
        'Боул',
        'Аранчини (указать кол-во)',
        '+ Модификаторы',
        'Картошка/Нагетсы/Другое (указать кол-во)',
        'Сезам откройся!'
    ]; // poll can have lte than 10 options

    const keyboard = Markup.inlineKeyboard(
        [Markup.button.callback('Закрыть голосование', 'stop_poll')]
    );

    ctx.telegram.sendPoll(chatId, 'It\'s shawarma time!', options, {
        is_anonymous: false,
        allows_multiple_answers: true,
        reply_markup: keyboard.reply_markup,
    }).then(() => {
        shawaMessage = ctx.message;
    });
});

bot.action(/.*/, (ctx) => {
    const creator = shawaMessage.from.id;
    const user_id = ctx.callbackQuery.from.id;
    console.log(creator, user_id);
    if (creator !== user_id) {
        ctx.answerCbQuery('Вы не открывали голосование, чтобы его закрывать :)');
        return;
    }

    ctx.telegram.stopPoll(ctx.callbackQuery.message.chat.id, ctx.callbackQuery.message.message_id).then(() => {
        shawaMessage = null;
    });
});

bot.launch();

// Enable graceful stop
process.once('SIGINT', () => bot.stop('SIGINT'))
process.once('SIGTERM', () => bot.stop('SIGTERM'))