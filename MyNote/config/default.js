window.config = {
  routerBasename: '/',
  servers: {
    dicomWeb: [
      {
        name: 'Orthanc',
        wadoUriRoot: 'http://172.28.119.119:8042/dicom-web',
        qidoRoot: 'http://172.28.119.119:8042/dicom-web',
        wadoRoot: 'http://172.28.119.119:8042/dicom-web',
        qidoSupportsIncludeField: true,
        imageRendering: 'wadors',
        thumbnailRendering: 'wadors',
        enableStudyLazyLoad: true,
        requestOptions: {
          auth: 'PatriciaXiao:patxiao2025' // basic auth if enabled
        }
      }
    ]
  }
};
