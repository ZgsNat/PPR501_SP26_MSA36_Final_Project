import { XMLParser } from 'fast-xml-parser';

const options = {
  ignoreAttributes: false,
  attributeNamePrefix: "@_",
  // Force 'student' to always be an array
  isArray: (name) => name === 'student'
};

const parser = new XMLParser(options);

export const parseXmlToJson = (xmlData) => {
  if (!xmlData) return null;
  try {
    return parser.parse(xmlData);
  } catch (e) {
    console.error("XML Parse Error", e);
    return null;
  }
};