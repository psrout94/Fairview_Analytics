import PostsRepository from './PostsRepository';

const repositories = {
  posts: PostsRepository,
  // other repositories ...
};

const RepositoryFactory = {
  get: (name) => repositories[name],
};

export { RepositoryFactory as default };
