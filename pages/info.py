import streamlit as st 
import os
import pandas as pd
from nav import navigation

#Page Config
st.set_page_config(
    layout = "wide",
    page_title="PIC IMS Fatal Error Guide",
    page_icon = "./assets/favi.ico",
)

#Navigation Bar:
with st.sidebar:
    navigation()

#Fatal Error Select Box
fatalerror_dict = {
    "PIC Error 4174": {
        "error_desc":"This is a new tenant in IMS-PIC. No 50058 data for the head of household exists. At least one new admission or historical adjustment record must be submitted first.",
        "link":"https://files.hudexchange.info/resources/documents/PIC-Error-4174-New-Tenant-Job-Aid.pdf"
    },
    "PIC Error 4080": {
        "error_desc":"A record with a later effective date exists in the database. Either remove the later record or change this effective date to a later date.",
        "link":"https://files.hudexchange.info/resources/documents/PIC-Error-4080-Later-Effective-Date-Job-Aid.pdf"
    },
    "PIC Error 5280": {
        "error_desc":"A record with a later effective date exists in the database. Either remove the later record or change this effective date to a later date.",
        "link":"https://files.hudexchange.info/resources/documents/PIC-Error-5280-Voucher-Record-Does-Not-Exist-Job-Aid.pdf"
    },
    "PIC Error 4182": {
        "error_desc":"This tenant already exists at this PHA in the IMS-PIC database. New admission cannot be accepted.",
        "link":"https://files.hudexchange.info/resources/documents/PIC-Error-4182-Tenant-Already-Exists-Job-Aid.pdf"
    },
    "PIC Error 4006": {
        "error_desc":"PHA code for tenant does not match with existing PHA code in database.",
        "link":"https://files.hudexchange.info/resources/documents/PIC-Error-4006-PHA-Code-Does-Not-Match-Job-Aid.pdf"
    }
}


st.markdown("""
<style>
/* ===== Global Page Styling ===== */
body {
    font-family: 'Inter', sans-serif;
    background-color: #0E1117;
    color: #E2E8F0;
}

/* ===== Hero Section ===== */
.hero {
    text-align: center;
    margin-bottom: 30px;
}

.hero h1 {
    font-size: 2.4rem;
    color: #93C5FD;
    font-weight: 800;
    letter-spacing: 1px;
    margin-top: -30px;
    margin-bottom: 10px;
}

.hero h4 {
    font-size: 1.1rem;
    font-weight: 400;
    color: #CBD5E1;
    max-width: 700px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ===== Section Styling ===== */
.section {
    text-align: center;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 18px;
    padding: 28px 40px;
    margin: 30px auto;
    max-width: 900px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.25);
    backdrop-filter: blur(6px);
}

.section h3 {
    font-size: 1.3rem;
    font-weight: 700;
    color: #F8FAFC;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 15px;
}

.section p {
    font-size: 1rem;
    color: #D1D5DB;
    line-height: 1.8;
    margin: 10px 0;
}

/* ===== Divider ===== */
.divider {
    width: 65%;
    height: 2px;
    background: linear-gradient(to right, transparent, #38BDF8, transparent);
    margin: 35px auto;
    border-radius: 2px;
}

/* ===== Call to Action ===== */
.call-to-action {
    text-align: center;
    font-size: 1.05rem;
    font-style: italic;
    text-decoration: underline;
    color: #F1F5F9;
    margin-top: 40px;
    margin-bottom: 30px;
    letter-spacing: 0.6px;
}
</style>

<div class="hero">
    <h1>PIC IMS Fatal Error Monitoring Guide</h1>
    <h4>
        A clear and structured overview to help Program Specialists understand, prevent, and resolve fatal errors 
        in the PIC IMS system to maintain compliance and data integrity.
    </h4>
</div>
""", unsafe_allow_html=True)


with st.container(horizontal_alignment = "center"):
    fatal_select = st.selectbox(
        "Fatal Error Type",
        fatalerror_dict, width = 350
    )

    st.markdown(
        f"<p style='text-align: center;'>Error Description: {fatalerror_dict[fatal_select]['error_desc']}</p>",
        unsafe_allow_html=True
    )

    st.link_button("Go To Solution",fatalerror_dict[fatal_select]["link"])


st.markdown("""
<div class='section'>
    <h3>Monitoring Fatal Errors in PIC IMS</h3>
    <p>
    Monitoring fatal errors in the PIC IMS system is essential for ensuring smooth workflows for Program Specialists. 
    Fatal errors occur when 50058 submissions contain issues or inconsistencies that prevent them from being successfully transmitted 
    through the PIC secure submission module.
    </p>
</div>
<div class='divider'></div>

<div class='section'>
    <h3>Impact of Unresolved Errors</h3>
    <p>
    Failing to address outstanding or unresolved errors can result in new admissions not being properly recorded by the 
    U.S. Department of Housing and Urban Development (HUD), which may restrict Enterprise Income Verification (EIV) access for affected clients. 
    </p>
    <p>
    Additionally, any subsequent changes to a 50058 form after an initial fatal error may not be transmitted to HUD, 
    creating transparency gaps between the Public Housing Authority (PHA) and HUD.
    </p>
</div>

<div class='divider'></div>

<div class='section'>
    <h3>Maintaining Data Integrity</h3>
    <p>
    Understanding the specific type of fatal error associated with a tenant’s 50058 form and knowing the most effective correction method 
    is critical to maintaining data integrity and compliance.
    </p>
</div>
""", unsafe_allow_html=True)