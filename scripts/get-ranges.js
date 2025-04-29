#!/usr/bin/env node

// Retrieves range information from ISBN International and stores it as an XML file.
// Shamelessly copied from https://github.com/inventaire/isbn3/blob/main/scripts/update_groups.js and adapted
//
// For manual download, visit: https://www.isbn-international.org/range_file_generation

const fs = require('fs')
const { promisify } = require('util')
const writeFile = promisify(fs.writeFile)
const { URLSearchParams } = require('url')

const domain = 'https://www.isbn-international.org'
const url = `${domain}/bl_proxy/GetRangeInformations`

const params = new URLSearchParams({
  format: 1,
  language: 'en',
  translatedTexts: 'Printed;Last Change'
})

const getFileUrl = async () => {
  const res = await fetch(url, { method: 'POST', body: params })
  const body = await res.json()
  const { filename, value } = body.result
  return `${domain}/download_range/${value}/${filename}`
}

console.log('Requesting XML ranges file...')
getFileUrl()
.then(fileUrl => {
  console.log(`Downloading ${fileUrl}...`)
  return fetch(fileUrl)
})
.then(res => res.text())
.then(res => writeFile('./src/data/ranges.xml', res))
.then(() => console.log('File saved: ./src/data/ranges.xml'))
