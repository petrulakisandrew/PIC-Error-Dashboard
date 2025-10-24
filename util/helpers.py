import random
import streamlit as st 
import pandas as pd
from db import check_pending_vendor

def generate_random_id(length=16):
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(chars) for _ in range(length))

def vendor_status_badge():
    status = check_pending_vendor()
    for row in status:
        if row [0] ==  False:
            return "⚠️"
    
    return "✅"