from kafka import KafkaProducer
import pandas as pd

# Kafka configuration
bootstrap_servers = []

username = "kafkaapi"
password = "kafkapi#123"
topic_name = "API_TEST"

producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    api_version=(0, 10, 1),
    security_protocol="SASL_SSL",
    sasl_mechanism="SCRAM-SHA-512",
    sasl_plain_username=username,
    sasl_plain_password=password,
    ssl_cafile="/home/manishkumar2.c/devtruststore_combined.pem",  # Use the converted PEM file here
    value_serializer=lambda v: v.encode("utf-8"),
    ssl_check_hostname=False
)

# Function to generate sample data
def generate_sample_data():
    # Creating a sample DataFrame with mock data
    data = {
        "id": [1, 2, 3, 4, 5],
        "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "age": [24, 27, 22, 32, 29],
        "city": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
    }
    df = pd.DataFrame(data)
    return df

# Function to produce data to Kafka
def produce_to_kafka():
    try:
        # Generate sample data
        df = generate_sample_data()
        # Convert DataFrame to JSON format
        json_records = df.to_json(orient="records", lines=True).splitlines()
        # Produce each record to Kafka
        for message in json_records:
            print(message)
            producer.send(topic_name, message)
            print("-----------------------------")
        producer.flush()  # Make sure all messages are sent
        print({"status": "success", "message": "Data sent to Kafka"})
    except Exception as e:
        print({"status": "error", "message": str(e)})

# Run the Kafka producer function
if __name__ == '__main__':
    produce_to_kafka()
