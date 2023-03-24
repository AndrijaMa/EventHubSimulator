from azure.servicebus import ServiceBusService
from random import randrange, random, choice
from datetime import datetime
import json
import time
import streamlit as st 


st.set_page_config(page_title='Azure Eventuhub simulator', layout = 'wide', initial_sidebar_state = 'auto')

num_devices = st.slider("Number of devices to simulate:", min_value=1,max_value=100, value=10, step=1);
shared_access_key_name = st.text_input("Shared access key name:", value="RootManageSharedAccessKey");
shared_access_key_value = st.text_input("Shared access key value:", type="password", );
service_namespace = st.text_input("Service name:", value="");
hub_name = st.text_input("Hub name:", value="");
sleep_time=st.slider("Sleep time:",min_value=0.01,max_value=1.00,step=0.01, value=0.01)


if st.button("Start simulation"):
    while True:
        try:
            sbs = ServiceBusService(service_namespace,
                        shared_access_key_name=shared_access_key_name,
                        shared_access_key_value=shared_access_key_value)
            msg = {}
            is_error = choice([True, False])
            device_id = randrange(1, num_devices)
            temperature = randrange(-50, 50) + random()
            pressure = randrange(0, 500) + random()
            ts = datetime.now().isoformat()
            msg["deviceId"] = "Device" + "-" + str(device_id)
            msg["temperature"] = temperature
            if not is_error:
                msg["pressure"] = pressure
            msg["ts"] = ts
            msg["source"] = "eventhub"

        
            sbs.send_event(hub_name, json.dumps(msg))
            time.sleep(sleep_time)

        except Exception as e:
            st.write(e)
            
