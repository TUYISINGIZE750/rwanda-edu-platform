export const TVET_TRADES = {
  'ICT & Technology': [
    'Software Development',
    'Computer Systems and Architecture',
    'Networking and Internet Technology',
    'Software Programming and Embedded Systems',
    'Multimedia Production'
  ],
  'Construction & Engineering': [
    'Building Construction',
    'Electrical Technology',
    'Electronics and Telecommunication',
    'Plumbing Technology',
    'Masonry',
    'Public Works',
    'Land Surveying',
    'Renewable Energy'
  ],
  'Manufacturing & Production': [
    'Manufacturing Technology',
    'Automobile Technology',
    'Wood Technology',
    'Leather Technology'
  ],
  'Hospitality & Tourism': [
    'Tourism',
    'Food and Beverage Operations',
    'Front Office and Housekeeping Operations'
  ],
  'Agriculture & Environment': [
    'Agriculture',
    'Animal Health',
    'Forestry',
    'Food Processing'
  ],
  'Arts & Design': [
    'Fashion Design',
    'Fine and Plastic Arts',
    'Interior Design',
    'Music and Performing Arts',
    'Tailoring'
  ],
  'Business & Finance': [
    'Accounting'
  ]
}

export const getAllTrades = () => {
  const trades = []
  Object.values(TVET_TRADES).forEach(category => {
    trades.push(...category)
  })
  return trades.sort()
}
