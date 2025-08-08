window.config = {
  routerBasename: '/',
  servers: {
    dicomWeb: [
      {
        name: 'Orthanc',
        wadoUriRoot: 'http://host.docker.internal:8042/dicom-web',
        qidoRoot: 'http://host.docker.internal:8042/dicom-web',
        wadoRoot: 'http://host.docker.internal:8042/dicom-web',
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
