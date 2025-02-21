import React from 'react'
import Select from 'react-select';
import monacoThemes from 'monaco-themes/themes/themelist.json';


const ThemeDropdown = ({ handleThemeChange, theme }) => {
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

            onChange={handleThemeChange}
        />
    )
}

export default ThemeDropdown