# weibolu-bot

Discord py bot for personal use.

## Some Features:
- [MyAnimeList anime/ manga lookup](#MyAnimeList-implementation:)
- Urban Dictionary lookup
- osu!track API integration
- Experience system
- Economy system
- Logging
- Guild specific configuration

```
<> : required
{} : optional

Do not include the actual brackets
```

### MyAnimeList implementation:

![anime embed](https://i.imgur.com/xdGDmno.png)

```
!anime <anime name> 
!manga <manga name> 
``` 
### Urban dictionary implementation:

` !define <term or expression> `

### Embed creation:

Fields values are seperated by '|'. To make a field inline, include 'i' at the end of the field.

i.e. `name1|value1|i name2|value2|i name3|value3`

`!embed <title> <desc> {color|0xHEX} {image|URL} {field_name|field_content|inline}`


![embed example](https://i.imgur.com/L3TXZAb.png)

## Plans
- Change API integrations to be fully async (aiohttp)
- Improve economy system - More things to buy, more minigames - etc.
- Migrate to the [subcommand system](https://discordpy.readthedocs.io/en/latest/faq.html#how-do-i-make-a-subcommand)
- Reactions/ auto role assignment