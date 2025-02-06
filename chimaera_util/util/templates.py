task_template = """
/** The ##task_name## task */
struct ##task_name## : public Task, TaskFlags<TF_SRL_SYM> {
  /** SHM default constructor */
  HSHM_INLINE explicit
  ##task_name##(const hipc::CtxAllocator<CHI_ALLOC_T> &alloc) : Task(alloc) {}

  /** Emplace constructor */
  HSHM_INLINE explicit
  ##task_name##(const hipc::CtxAllocator<CHI_ALLOC_T> &alloc,
                const TaskNode &task_node,
                const PoolId &pool_id,
                const DomainQuery &dom_query) : Task(alloc) {
    // Initialize task
    task_node_ = task_node;
    prio_ = TaskPrioOpt::kLowLatency;
    pool_ = pool_id;
    method_ = Method::##method_enum_name##;
    task_flags_.SetBits(0);
    dom_query_ = dom_query;

    // Custom
  }

  /** Duplicate message */
  void CopyStart(const ##task_name## &other, bool deep) {
  }

  /** (De)serialize message call */
  template<typename Ar>
  void SerializeStart(Ar &ar) {
  }

  /** (De)serialize message return */
  template<typename Ar>
  void SerializeEnd(Ar &ar) {
  }
};
"""

client_method_template = """
/** ##method_name## task */
void ##method_name##(const hipc::CtxAllocator<CHI_ALLOC_T> &alloc,
                     const DomainQuery &dom_query) {
  FullPtr<##task_name##> task =
    Async##method_name##(dom_query);
  task->Wait();
  CHI_CLIENT->DelTask(mctx, task);
}
CHI_TASK_METHODS(##method_name##);
"""

runtime_method_template = """
  /** The ##method_name## method */
  void ##method_name##(##task_name## *task, RunContext &rctx) {
    task->SetModuleComplete();
  }
  void Monitor##method_name##(MonitorModeId mode, ##task_name## *task, RunContext &rctx) {
    switch (mode) {
      case MonitorMode::kReplicaAgg: {
        std::vector<FullPtr<Task>> &replicas = *rctx.replicas_;
      }
    }
  }
"""