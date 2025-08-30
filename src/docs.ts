const doc = {
  info: {
    title: "imnyang's Personal API",
    description: "Neko is cute.",
    version: "1.0.0",
    contact: {
      name: "HyunSuk Nam",
      url: "https://imnya.ng",
      email: "support@orygonix.com"
    },
    license: {
      name: "CC0-1.0 license",
      url: "https://creativecommons.org/publicdomain/zero/1.0/",
    }
  },
  servers: process.env.NODE_ENV === 'development' ? [
    {
      url: 'https://api.imnya.ng',
      description: "Production server"
    },
    {
      url: 'http://localhost:1108',
      description: "Local server"
    }
  ] : [

    {
      url: 'http://localhost:1108',
      description: "Local server"
    },
    {
      url: 'https://api.imnya.ng',
      description: "Production server"
    }
  ]
};

export default doc;