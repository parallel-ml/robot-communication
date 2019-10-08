import argparse
import asyncio
import os
import pickle
from concurrent.futures.thread import ThreadPoolExecutor
from contextlib import asynccontextmanager
from typing import List

from hbmqtt.client import QOS_2, MQTTClient
from hbmqtt.mqtt.publish import PublishPacket, PublishPayload
from hbmqtt.session import ApplicationMessage

label = ""


@asynccontextmanager
async def connect_to_broker(broker: str):
    try:
        client = MQTTClient(config=dict(keep_alive=240))
        await client.connect(broker)
        yield client
    finally:
        await client.disconnect()


async def subscribe_to_topics(client: MQTTClient, topics: List[str]):
    try:
        await client.subscribe([(topic, QOS_2) for topic in topics])
        while True:
            message = await client.deliver_message()
            packet: PublishPacket = message.publish_packet
            if packet:
                yield packet.topic_name, pickle.loads(packet.data)
    finally:
        await client.unsubscribe(topics)  # do not need the QOS for unsub


async def publish_to_topics(client: MQTTClient, topics: List[str], data):
    await asyncio.gather(
        *[
            asyncio.create_task(client.publish(topic, pickle.dumps(data), qos=QOS_2))
            for topic in topics
        ]
    )


async def subscribe_to_topics_task(client: MQTTClient, topics: List[str]):
    async for topic, message in subscribe_to_topics(client, topics):
        global label
        l = f"[{label}] " if label else ""
        print(f"{l}Recieved the following message in '{topic}': {message}")


async def publish_to_topics_task(client: MQTTClient, topics: List[str]):
    i = 0
    while True:
        await publish_to_topics(client, topics, f"i is {i}")
        await asyncio.sleep(1)
        i += 1


async def main():
    parser = argparse.ArgumentParser(description="MQTT Client")
    parser.add_argument("--label", help="The log label of this process.", type=str)
    parser.add_argument(
        "--broker", help="The MQTT broker to connect to.", type=str, required=True
    )
    parser.add_argument(
        "--topics-publish",
        nargs="*",
        help="List of topics to subscribe to.",
        type=str,
        default=[],
    )
    parser.add_argument(
        "--topics-subscribe",
        nargs="*",
        help="List of topics to subscribe to.",
        type=str,
        default=[],
    )
    args = parser.parse_args()
    global label
    label = args.label

    async with connect_to_broker(args.broker) as client:
        subscribe_task = asyncio.create_task(
            subscribe_to_topics_task(client, args.topics_subscribe)
        )
        await asyncio.sleep(0.5)
        await asyncio.gather(
            subscribe_task,
            asyncio.create_task(publish_to_topics_task(client, args.topics_publish)),
        )


if __name__ == "__main__":
    asyncio.run(main())
