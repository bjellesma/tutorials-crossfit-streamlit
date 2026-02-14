"""Streamlit application router for CrossFit data visualization.

This module provides navigation between dashboard and athlete profile pages.
"""

import streamlit as st
import utils.logger as logger

logger = logger.get_logger(__name__)


def main():
    """Run the Streamlit application with navigation support.

    Uses st.navigation() to route between dashboard and profile pages.
    Provides proper multi-page app structure with hidden navigation UI.

    """
    # Define pages
    logger.debug('Starting Streamlit application')
    dashboard = st.Page('pages/dashboard.py', title='Dashboard', icon='📊', default=True)
    profile = st.Page('pages/profile.py', title='Athlete Profile', icon='👤')

    pg = st.navigation([dashboard, profile], position='top')

    # Run the selected page
    pg.run()


if __name__ == '__main__':
    main()
