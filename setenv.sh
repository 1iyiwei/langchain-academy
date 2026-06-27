#!/bin/bash
for i in {1..5}; do
  cp module-$i/studio/.env.example module-$i/studio/.env
  echo "OPENAI_API_KEY=\"$OPENAI_API_KEY\"" > module-$i/studio/.env
  echo "GOOGLE_API_KEY=\"$GOOGLE_API_KEY\"" >> module-$i/studio/.env
  echo "XAI_API_KEY=\"$XAI_API_KEY\"" >> module-$i/studio/.env
done
echo "TAVILY_API_KEY=\"$TAVILY_API_KEY\"" >> module-4/studio/.env
