const Discord = require('discord.js');
const superagent = require('superagent')
const config = require('./config.json')

const client = new Discord.Client();

client.on('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
});

client.on('message', msg => {
  if (msg.content === '!kamervanjens') {
        superagent.get("https://temp.jensderuiter.dev/").then((res) => {
            let embed = new Discord.RichEmbed()
                .setTitle("Jens' Kamer")
                .setFooter("Jens de Ruiter")
                .setColor("#e34646")
                .setDescription("Wat voor nut had dit ook alweer?")
                .addField(`${res.body.data.temperature}℃`, "Dit is de temperatuur in mijn kamer.")
                .addField(`${res.body.data.humidity}%`, "Dit is de luchtvochtigheid in mijn kamer.");
            msg.channel.send({embed});
        });
  }
});

client.login(config.token);