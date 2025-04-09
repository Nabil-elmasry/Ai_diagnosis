
def extract_sensor_data(text):
    lines = text.split('\n')
    sensors = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 4:
            name = ' '.join(parts[:-3])
            value = parts[-3]
            standard = parts[-2]
            unit = parts[-1]
            sensors.append([name, value, standard, unit])
    return pd.DataFrame(sensors, columns=["Sensor", "Value", "Standard", "Unit"])

