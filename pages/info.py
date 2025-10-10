import streamlit as st 
import os

st.set_page_config(
    layout = "wide"
)

#Title for Information Page
st.markdown("<h1 style='text-align: center;'>Helpful Information</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>How to Correct your Fatal Errors</h1>", unsafe_allow_html=True)
st.divider()

#Body Text
st.markdown("<h6 style='text-align: center;'>Monitoring fatal errors in the PIC IMS system is essential for ensuring smooth workflows for Program Specialists. Fatal errors occur when 50058 submissions contain issues or inconsistencies that prevent them from being successfully transmitted through the PIC secure submission module.Monitoring fatal errors in the PIC IMS system is essential for ensuring smooth workflows for Program Specialists. Fatal errors occur when 50058 submissions contain issues or inconsistencies that prevent them from being successfully transmitted through the PIC secure submission module.Monitoring fatal errors in the PIC IMS system is essential for ensuring smooth workflows for Program Specialists. Fatal errors occur when 50058 submissions contain issues or inconsistencies that prevent them from being successfully transmitted through the PIC secure submission module.</h6>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;'>Failing to address outstanding or unresolved errors can result in new admissions not being properly recorded by the U.S. Department of Housing and Urban Development (HUD), which may, in turn, restrict Enterprise Income Verification (EIV) access for affected clients. Additionally, any subsequent changes to a 50058 form after an initial fatal error may not be transmitted to HUD, creating transparency gaps between the Public Housing Authority (PHA) and HUD.</h6>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;'>Understanding the specific type of fatal error associated with a tenant’s 50058 form and knowing the most effective correction method is critical to maintaining data integrity and compliance.</h6>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center; text-decoration: underline;'><em>Please see below for an explanation of each type of fatal error and what it means.</em></h6>", unsafe_allow_html=True)
st.divider()