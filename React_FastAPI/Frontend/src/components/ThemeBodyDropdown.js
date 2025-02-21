import React from 'react'
import Select from 'react-select';
import { customStyles } from '../constants/customStyles';

const ThemeBodyDropdown = ({ handleThemeChange, theme }) => {
    const themes = Object.entries(monacoThemes);

    const themeOptions = themes.map(([themeId, themeName]) => ({
        label: themeName,
        value: themeId,
        key: themeId
    }))
    return (
        <Select
            placeholder='Select Theme'
            options={themeOptions}
            value={theme}
            styles={customStyles}
            onChange={handleThemeChange}
        />
    )
}

export default ThemeBodyDropdown