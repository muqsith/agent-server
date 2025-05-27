# deepwiki.py

from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from agents.exceptions import InputGuardrailTripwireTriggered
from agents.mcp import MCPServerSse
from pydantic import BaseModel

class WeatherGuardrailOutput(BaseModel):
    is_weather: bool
    reasoning: str

weather_guardrail_agent = Agent(
    name="Weather Guardrail",
    instructions="Check if the user's question is about the weather. Respond true if it is about weather, temperature, forecast, rain, snow, humidity, wind, climate, storm, sunny, cloudy, or precipitation.",
    output_type=WeatherGuardrailOutput,
)

async def weather_guardrail(ctx, agent, input_data):
    result = await Runner.run(weather_guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(WeatherGuardrailOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_weather,
    )

deepwiki_agent = None
mcp_server = None

async def setup_weather():
    global deepwiki_agent, mcp_server
    mcp_server = await MCPServerSse(
        name="Weather",
        params={"url": "http://localhost:8053/sse"}
    ).__aenter__()

    deepwiki_agent = Agent(
        name="WeatherAgent",
        instructions="You are a helpful assistant with weather tools.",
        mcp_servers=[mcp_server],
        input_guardrails=[
            InputGuardrail(guardrail_function=weather_guardrail),
        ],
    )

async def cleanup_weather():
    global mcp_server
    if mcp_server:
        await mcp_server.__aexit__(None, None, None)

async def handle_weather_query(message: str) -> str:
    if deepwiki_agent is None:
        raise RuntimeError("Weather agent not initialized")
    try:
        result = await Runner.run(starting_agent=deepwiki_agent, input=message)
        return result.final_output
    except InputGuardrailTripwireTriggered as e:
        return "Sorry, I can only answer questions related to the weather."
