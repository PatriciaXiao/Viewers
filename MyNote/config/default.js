window.config = {
  dataSources: [
    {
      namespace: '@ohif/extension-default.dataSourcesModule.dicomweb',
      sourceName: 'orthancProxy',
      configuration: {
        wadoUriRoot: 'http://172.28.119.119:8043/dicom-web',
        qidoRoot: 'http://172.28.119.119:8043/dicom-web',
        wadoRoot: 'http://172.28.119.119:8043/dicom-web',
        // No need for auth here, since nginx adds it
        supportsFuzzyMatching: true,
        enableStudyLazyLoad: true,
        imageRendering: 'wadors',
      },
    },
  ],
};
