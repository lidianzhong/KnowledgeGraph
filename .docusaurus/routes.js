import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/KnowledgeGraph/__docusaurus/debug',
    component: ComponentCreator('/KnowledgeGraph/__docusaurus/debug', 'b67'),
    exact: true
  },
  {
    path: '/KnowledgeGraph/__docusaurus/debug/config',
    component: ComponentCreator('/KnowledgeGraph/__docusaurus/debug/config', '840'),
    exact: true
  },
  {
    path: '/KnowledgeGraph/__docusaurus/debug/content',
    component: ComponentCreator('/KnowledgeGraph/__docusaurus/debug/content', '2fc'),
    exact: true
  },
  {
    path: '/KnowledgeGraph/__docusaurus/debug/globalData',
    component: ComponentCreator('/KnowledgeGraph/__docusaurus/debug/globalData', '584'),
    exact: true
  },
  {
    path: '/KnowledgeGraph/__docusaurus/debug/metadata',
    component: ComponentCreator('/KnowledgeGraph/__docusaurus/debug/metadata', 'bae'),
    exact: true
  },
  {
    path: '/KnowledgeGraph/__docusaurus/debug/registry',
    component: ComponentCreator('/KnowledgeGraph/__docusaurus/debug/registry', '220'),
    exact: true
  },
  {
    path: '/KnowledgeGraph/__docusaurus/debug/routes',
    component: ComponentCreator('/KnowledgeGraph/__docusaurus/debug/routes', 'f6e'),
    exact: true
  },
  {
    path: '/KnowledgeGraph/markdown-page',
    component: ComponentCreator('/KnowledgeGraph/markdown-page', 'f46'),
    exact: true
  },
  {
    path: '/KnowledgeGraph/docs',
    component: ComponentCreator('/KnowledgeGraph/docs', 'f71'),
    routes: [
      {
        path: '/KnowledgeGraph/docs',
        component: ComponentCreator('/KnowledgeGraph/docs', 'c35'),
        routes: [
          {
            path: '/KnowledgeGraph/docs',
            component: ComponentCreator('/KnowledgeGraph/docs', 'f17'),
            routes: [
              {
                path: '/KnowledgeGraph/docs/category/开始上手',
                component: ComponentCreator('/KnowledgeGraph/docs/category/开始上手', '65e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/KnowledgeGraph/docs/category/项目文档',
                component: ComponentCreator('/KnowledgeGraph/docs/category/项目文档', '190'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/KnowledgeGraph/docs/documents/document-intro',
                component: ComponentCreator('/KnowledgeGraph/docs/documents/document-intro', 'fde'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/KnowledgeGraph/docs/documents/software-detailed-design-specification',
                component: ComponentCreator('/KnowledgeGraph/docs/documents/software-detailed-design-specification', 'cd3'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/KnowledgeGraph/docs/documents/software-requirements-specification',
                component: ComponentCreator('/KnowledgeGraph/docs/documents/software-requirements-specification', '454'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/KnowledgeGraph/docs/documents/software-summary-design-specification',
                component: ComponentCreator('/KnowledgeGraph/docs/documents/software-summary-design-specification', '5b5'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/KnowledgeGraph/docs/documents/software-test-report',
                component: ComponentCreator('/KnowledgeGraph/docs/documents/software-test-report', '81e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/KnowledgeGraph/docs/intro',
                component: ComponentCreator('/KnowledgeGraph/docs/intro', 'adb'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/KnowledgeGraph/docs/start/install',
                component: ComponentCreator('/KnowledgeGraph/docs/start/install', '324'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/KnowledgeGraph/',
    component: ComponentCreator('/KnowledgeGraph/', 'dbb'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
