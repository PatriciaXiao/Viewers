window.config = {
  routerBasename: '/',
  servers: {
    dicomWeb: [
      {
        name: 'Orthanc',
        wadoUriRoot: 'http://172.28.119.119:8042/wado',
        qidoRoot: 'http://172.28.119.119:8042/dicom-web',
        wadoRoot: 'http://172.28.119.119:8042/dicom-web',
        qidoSupportsIncludeField: true,
        imageRendering: 'wadors',
        thumbnailRendering: 'wadors',
        enableStudyLazyLoad: true,
        requestOptions: {
          auth: 'orthanc:orthanc' // basic auth if enabled
        }
      }
    ]
  }
};
