# pysc2-protossbot

This will be our bot

## Running the bot.

`cd` into the directory for whichever bot you want to run

run the following command

```
python -m pysc2.bin.agent \
--map Simple64 \
--agent bot.PGSSProtoss \
--agent_race protoss \
--agent2 pysc2.agents.random_agent.RandomAgent \
--use_feature_units
```

